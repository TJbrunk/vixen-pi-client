using System;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Kadmium_sACN;
using Kadmium_sACN.SacnReceiver;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace VixenClient {
    internal class SacnListener : BackgroundService {
        private readonly ILogger<SacnListener> _logger;
        private readonly ClientConfig _configuration;
        private readonly MulticastSacnReceiverIPV4 _receiver;

        public SacnListener(ILogger<SacnListener> logger, ClientConfig config) {
            this._logger = logger;
            this._configuration = config;
            this._receiver = new MulticastSacnReceiverIPV4();
        }

        protected override Task ExecuteAsync(CancellationToken stoppingToken) {
            this._logger.LogInformation("SacnListener starting");
            this._receiver.OnDataPacketReceived += this.Receiver_OnDataPacketReceived;
            this._receiver.Listen(IPAddress.Any);
            this._receiver.JoinMulticastGroup(this._configuration.Universe);
            return Task.CompletedTask;
        }

        private void Receiver_OnDataPacketReceived(object sender, DataPacket dataPacket) {
            var universe = dataPacket.FramingLayer.Universe.ToString();
            this._logger.LogInformation("New packet received for universe " + universe);
            this._logger.LogInformation(string.Join(",", dataPacket.DMPLayer.PropertyValues));
        }

        public override Task StopAsync(CancellationToken cancellationToken) {
            this._logger.LogInformation("Shutting down listener");
            this._receiver.Dispose();
            base.StopAsync(cancellationToken);
            return Task.CompletedTask;
        }
    }
}
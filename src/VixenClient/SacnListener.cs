using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace VixenClient {
    internal class SacnListener : BackgroundService {
        private readonly ILogger<SacnListener> _logger;
        private readonly ClientConfig _configuration;

        public SacnListener(ILogger<SacnListener> logger, ClientConfig config) {
            this._logger = logger;
            this._configuration = config;
        }
        protected override async Task ExecuteAsync(CancellationToken stoppingToken) {
            this._logger.LogInformation("SacnListener starting");

            while(!stoppingToken.IsCancellationRequested) {
                this._logger.LogInformation("Loop execution");
                await Task.Delay(TimeSpan.FromSeconds(10));
            }
            this._logger.LogInformation("Loop shutdown");
        }
    }
}
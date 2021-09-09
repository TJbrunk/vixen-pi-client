using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Configuration;

namespace VixenClient {
    internal class Program {

        internal static async Task Main(string[] args) {
            using var host = CreateHostBuilder(args)
                .Build();

            await host.RunAsync();
        }

        internal static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
            .ConfigureServices(sc => {
                sc.AddSingleton(sc => {
                    using var scope = sc.CreateScope();
                    var config = sc.GetRequiredService<IConfiguration>();
                    var clientConfig = new ClientConfig();
                    config.GetSection("ClientConfig").Bind(clientConfig);
                    return clientConfig;
                });
                sc.AddHostedService<SacnListener>();
                //sc.Configure<ClientConfig>(x => x.);
            });
    }
}

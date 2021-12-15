using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;

namespace ResiliencePatterns.Polly
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddLogging().AddControllers().AddJsonOptions(opt =>
            {
                opt.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
            });

            var readTimeout = Environment.GetEnvironmentVariable("READ_TIMEOUT") ?? "0";
            var backendHost = Environment.GetEnvironmentVariable("BACKEND_HOST") ?? "http://localhost:9211";
            var resourcePath = Environment.GetEnvironmentVariable("RESOURCE_PATH") ?? "/status/200";

            // logger.LogInformation("Read timeout is {0}.", readTimeout);
            // logger.LogInformation("Backend host is {0}.", backendHost);
            // logger.LogInformation("Resource is {0}.", resourcePath);

            services.AddHttpClient("backend", c =>
            {
                c.BaseAddress = new Uri(backendHost);
                c.Timeout = TimeSpan.FromMilliseconds(Int32.Parse(readTimeout));
            });
            services.AddScoped<BackendService>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseRouting();
            app.UseAuthorization();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}

using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using Microsoft.Extensions.Logging;

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
            services.AddLogging(opt => 
            {
                opt.AddConsole(c => {
                    c.TimestampFormat = "yyyy-MM-dd HH:mm:ss";
                });
            }).AddControllers().AddJsonOptions(opt =>
            {
                opt.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
            });

            var readTimeout = Environment.GetEnvironmentVariable("READ_TIMEOUT") ?? "0";
            var backendHost = Environment.GetEnvironmentVariable("BACKEND_HOST") ?? "http://localhost:9211";

            services.AddHttpClient("backend", c =>
            {
                if (readTimeout != "0")
                {
                   c.Timeout = TimeSpan.FromMilliseconds(Int32.Parse(readTimeout)); 
                }
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

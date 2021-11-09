FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build-env
WORKDIR /app

COPY ResiliencePatterns.Polly.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish ResiliencePatterns.Polly.csproj -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "ResiliencePatterns.Polly.dll"]

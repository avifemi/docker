var builder = WebApplication.CreateBuilder(args);
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(5000);
});
var app = builder.Build();
app.MapGet("/", () => "Hello World!");

app.Run();
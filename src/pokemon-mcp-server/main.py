from mcp.server.fastmcp import FastMCP
from settings import get_settings

settings = get_settings()
mcp = FastMCP(
    name="Pokemon MCP Server",
    log_level=settings.log_level,
    host=settings.host,
    port=settings.port,
)


@mcp.tool()
async def get_pokemon(pokemon: str) -> dict:
    """Get information about a specific Pokémon.

    Args:
        pokemon: The name or ID of the Pokémon to fetch information for.
    """
    from utils.request import request_get

    try:
        data = await request_get(f"pokemon/{pokemon}")
        return data
    except Exception as e:
        return f"Error fetching data for {pokemon}: {e}"

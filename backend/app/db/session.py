from typing_extensions import NoExtraItems
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

class DatabaseManager:
    client: AsyncMongoClient | None = None

    async def connect_to_database(self, uri: str) -> None:
        """Initializes the AsyncMongoClient and verifies connection with a ping."""
        self.client = AsyncMongoClient(uri)
        await self.client.admin.command("ping")
    
    async def close_database_connection(self) -> None:
        """closes the mongodb connection pool cleanly."""
        if self.client is not None :
            await self.client.close()
            self.client = None
    
    def get_database(self, db_name:str):
        """Returns the targeted database instance"""
        if self.client is None:
            raise RuntimeError("Database client not initialise . call connect_to_database first...")
        return self.client[db_name]

db_manager = DatabaseManager()
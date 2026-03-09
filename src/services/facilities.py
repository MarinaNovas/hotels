from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService

class FacilitiesService(BaseService):
    async def create_facility(self, data: FacilityAdd):
        result = await self.db.facilities.add(data)
        await self.db.commit()
        # test_task.delay()
        return result

    async def get_facilities(self):
        return await self.db.facilities.get_all()
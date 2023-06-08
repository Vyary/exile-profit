from typing import Any, Dict
from tqdm import tqdm
from gems.gem_builder import GemBuilder
from items.corrupted_gem import CorruptedGem
from items.leveled_gem import LeveledGem
from storages.item_storage import ItemStorage


class GemBuildManager:
    def gem_info(
        self,
        gem_queries: Dict[str, Any],
        gem_builder: GemBuilder,
        storage: ItemStorage,
    ):
        corrupted_gem_repository = storage.new_storage()
        leveled_gem_repository = storage.new_storage()

        for gem_name, gem_types in tqdm(gem_queries.items(), desc="Gems"):
            if len(gem_types["components"].items()) < 5:
                buy, leveled, fail, success = gem_types["components"].items()
                vaal = (None, None)
            else:
                buy, leveled, fail, success, vaal = gem_types["components"].items()

            complete_corrupted_gem = gem_builder.build_corrupted_gem(
                CorruptedGem(), gem_name, buy, fail, success, vaal
            )
            complete_leveled_gem = gem_builder.build_leveled_gem(
                LeveledGem(), gem_name, buy, leveled
            )

            corrupted_gem_repository.add_item(complete_corrupted_gem)
            leveled_gem_repository.add_item(complete_leveled_gem)

        return corrupted_gem_repository.inventory, leveled_gem_repository.inventory

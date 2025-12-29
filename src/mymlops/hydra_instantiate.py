import logging

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

log = logging.getLogger(__name__)


class MyClass:
    def __init__(self, name: str) -> None:
        self.name = name

    def say_hello(self) -> None:
        log.info(f"Hello, {self.name}!")


@hydra.main(config_path=".", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    myclass = MyClass("Greg")
    myclass.say_hello()

    myclass_hydra = instantiate(config.my_class)
    myclass_hydra.say_hello()


if __name__ == "__main__":
    main()

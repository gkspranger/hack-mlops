import logging

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


@hydra.main(config_path="configs", config_name="hydra_config", version_base=None)
def main(config: DictConfig) -> None:
    print(OmegaConf.to_yaml(config))


if __name__ == "__main__":
    main()

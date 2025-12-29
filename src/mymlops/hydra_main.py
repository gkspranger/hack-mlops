import logging
import os

import hydra
from hydra.utils import get_original_cwd, to_absolute_path
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


@hydra.main(config_path="configs", config_name="config", version_base="1.1")
def main(config: DictConfig) -> None:
    print(OmegaConf.to_yaml(config))
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")

    orig_cwd_abs = to_absolute_path(get_original_cwd())
    print(f"Original Current Working Directory: {orig_cwd_abs}")

    log.info("showing the log")
    log.error("now showing some error")


if __name__ == "__main__":
    main()

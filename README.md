# hack-mlops

## DVC

let's think about this .. i use `dvc add` to add mods to my dataset .. which in turns updates the related `.dvc` file ..

so for example, v1:

`dvc add data/data.xml`

- this data is local to the command

- let' hypothesize a similar MVS dataset name would be `MYHLQ.DATA.DATAXML`

```yaml
# data.xml.dvc output
outs:
- md5: 22a1a2931c8370d3aeedd7183606fd7f
  size: 14445097
  hash: md5
  path: data.xml
```

imagine dataset has been updated, and so now v2:

`dvc add data/data.xml`

- again, this data is local to the command

- so if this were an MVS dataset, would it always have to be `MYHLQ.DATA.DATAXML` ?? what if the dataset name has changed but i want this to continue to be represented as the original (i.e. `data/data.xml`) ??

```yaml
# data.xml.dvc output
outs:
- md5: 079fbd15fa2c32c539c4c4e3675b514a
  size: 28890194
  hash: md5
  path: data.xml
```

ok, so i get it's basically taking the MD5 of the file and using that to write to local/cache -- but those names were already `data/data.xml`

here's a look at the underlying FS, after a `dvc push`:

```shell
$ tree ~/tmp/dvcstore/files/md5/
/home/gks/tmp/dvcstore/files/md5/
├── 07
│   └── 9fbd15fa2c32c539c4c4e3675b514a
└── 22
    └── a1a2931c8370d3aeedd7183606fd7f
```

- i think understanding in how an s3 bucket/object is configed/pulled/used will help

## Hydra

### Command Line Injection

```python
# assume main.py prints config as YAML
python main.py +experiment.lr=5

experiment:
  lr: 5
```

### Grouping Config Files

```shell
$ tree configs
configs
├── __init__.py
├── config-merge.yaml
├── config.yaml
└── experiment
    ├── experiment-w-resent18.yaml
    └── experiment-w-resent50.yaml

# can define defaults, merges, and additional configs
$ python main.py experiment.hello=777
```

### Multirun

```shell
myml-hydra-main -m experiment=experiment-w-resent18,experiment-w-resent50

[2025-12-23 13:42:41,768][HYDRA] Launching 2 jobs locally
[2025-12-23 13:42:41,768][HYDRA]        #0 : experiment=experiment-w-resent18
experiment:
  hello: 999
  world: World!
some_key:
  some_value: 123

[2025-12-23 13:42:41,829][HYDRA]        #1 : experiment=experiment-w-resent50
experiment:
  hello: 999
  world: World!
some_key:
  some_value: 123
```

- many runs over many configs

```shell
$ myml-hydra-main -m experiment=experiment-w-resent18,experiment-w-resent50 loss_function=arface,surface
[2025-12-23 13:46:21,212][HYDRA] Launching 4 jobs locally
[2025-12-23 13:46:21,213][HYDRA]        #0 : experiment=experiment-w-resent18 loss_function=arface
experiment:
  hello: 999
  world: World!
loss_function:
  loss: arface
some_key:
  some_value: 123

[2025-12-23 13:46:21,274][HYDRA]        #1 : experiment=experiment-w-resent18 loss_function=surface
experiment:
  hello: 999
  world: World!
loss_function:
  loss: surface
some_key:
  some_value: 123

[2025-12-23 13:46:21,330][HYDRA]        #2 : experiment=experiment-w-resent50 loss_function=arface
experiment:
  hello: 999
  world: World!
loss_function:
  loss: arface
some_key:
  some_value: 123

[2025-12-23 13:46:21,394][HYDRA]        #3 : experiment=experiment-w-resent50 loss_function=surface
experiment:
  hello: 999
  world: World!
loss_function:
  loss: surface
some_key:
  some_value: 123
```

- can also be expressed as:

```shell
$ myml-hydra-main -m experiment='glob(*)' loss_function='glob(*, exclude=soft)'
```

### Logging

- simple since it hooks into main logging module

- will log to screen and to a file (which we may want to store later)

- can also set hydra options via CLI

```shell
$ myml-hydra-main hydra.verbose=true

[2025-12-29 09:45:52,978][HYDRA] Hydra 1.3.2
[2025-12-29 09:45:52,978][HYDRA] ===========
[2025-12-29 09:45:52,978][HYDRA] Installed Hydra Plugins
[2025-12-29 09:45:52,978][HYDRA] ***********************
[2025-12-29 09:45:52,978][HYDRA]        ConfigSource:
[2025-12-29 09:45:52,978][HYDRA]        -------------
[2025-12-29 09:45:52,978][HYDRA]                FileConfigSource
[2025-12-29 09:45:52,978][HYDRA]                ImportlibResourcesConfigSource
[2025-12-29 09:45:52,978][HYDRA]                StructuredConfigSource
[2025-12-29 09:45:52,978][HYDRA]        CompletionPlugin:
[2025-12-29 09:45:52,978][HYDRA]        -----------------
...
/home/gks/git/hack-mlops/.venv/lib/python3.12/site-packages/hydra/_internal/hydra.py:119: UserWarning: Future Hydra versions will no longer change working directory at job runtime by default.
See https://hydra.cc/docs/1.2/upgrades/1.1_to_1.2/changes_to_job_working_dir/ for more information.
  ret = run_job(
experiment:
  hello: 999
  world: World!
loss_function:
  loss: arface
some_key:
  some_value: 123

Current Working Directory: /home/gks/git/hack-mlops/outputs/2025-12-29/09-45-52
Original Current Working Directory: /home/gks/git/hack-mlops
[2025-12-29 09:45:53,131][mymlops.hydra_main][INFO] - showing the log
[2025-12-29 09:45:53,131][mymlops.hydra_main][ERROR] - now showing some error
```

### Debugging

- can inspect config values without executing the code

- print config to screen

```shell
$ myml-hydra-main --cfg job

experiment:
  hello: 999
  world: World!
loss_function:
  loss: arface
some_key:
  some_value: 123
```

- print hydra configs to screen

```shell
$ myml-hydra-main --cfg hydra

hydra:
  run:
    dir: outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}
  sweep:
    dir: multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
    subdir: ${hydra.job.num}
  launcher:
    _target_: hydra._internal.core_plugins.basic_launcher.BasicLauncher
  sweeper:
    _target_: hydra._internal.core_plugins.basic_sweeper.BasicSweeper
    max_batch_size: null
    params: null
  hydra_logging:
    version: 1
    formatters:
      simple:
        format: '[%(asctime)s][HYDRA] %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple
        stream: ext://sys.stdout
...
  runtime:
    version: 1.3.2
    version_base: '1.1'
    cwd: /home/gks/git/hack-mlops
    config_sources:
    - path: hydra.conf
      schema: pkg
      provider: hydra
    - path: mymlops.configs
      schema: pkg
      provider: main
    - path: ''
      schema: structured
      provider: schema
    output_dir: ???
    choices:
      loss_function: arface
      experiment: experiment-w-resent18
      hydra/env: default
      hydra/callbacks: null
      hydra/job_logging: default
      hydra/hydra_logging: default
      hydra/hydra_help: default
      hydra/help: default
      hydra/sweeper: basic
      hydra/launcher: basic
      hydra/output: default
  verbose: false
```

- there is an `all` option

- can test overiding configs via the command line

```shell
$ myml-hydra-main experiment.hello=777 --cfg job

experiment:
  hello: 777
  world: World!
loss_function:
  loss: arface
some_key:
  some_value: 123
```

### Instantiate

- can instantiate class defs defined in configs and doesn't have to be in code

- can instantiate any class really, doesn't have to be custom code

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

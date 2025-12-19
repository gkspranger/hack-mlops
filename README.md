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

# modlo-creator-version

The latest version of [Modlo Creator](https://modlocreator.app) and its changelog. On launch the app reads
[`version.json`](version.json) from this repository:

```
https://raw.githubusercontent.com/RatPrez/modlo-creator-version/main/version.json
```

When `latest` is newer than the running version, the app shows the changes since that version and a button that opens
`download_url`. Nothing is sent to the app's author: the request is a plain download of this file from GitHub.

## Publishing a release

1. Upload the new build where `download_url` points.
2. In `version.json`, set `latest` to the new version and add its entry at the top of `changelog`:

```json
{
  "latest": "1.0.1",
  "download_url": "https://polar.sh/modlocreator/portal",
  "changelog": [
    { "version": "1.0.1", "date": "2026-10-20", "changes": ["Walls drawn in a line join into one wall."] },
    { "version": "1.0.0", "date": "2026-10-16", "changes": ["First release."] }
  ]
}
```

3. Commit and push. The check in `.github/workflows/check.yml` fails if the file would not be understood by the app.

Versions are `major.minor.patch`. `latest` must equal the first entry of `changelog`, and the entries go from newest to
oldest.

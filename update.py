import requests
import json

# URL for the GitHub API to get releases
url = "https://api.github.com/repos/thongtech/go-legacy-win7/releases"

response = requests.get(url)
releases_data = response.json()

releases = []

versions = set()

for release in releases_data:
    tag_name = release['tag_name']
    version = tag_name.replace('v', '').split('-')[0]  # Extract version from tag
    if (version in versions):
        continue
    else:
        versions.add(version)
    stable = True  # Assuming all fetched versions are stable
    release_url = release['html_url']

    files = []
    for asset in release['assets']:
        filename = asset['name']
        #arch, platform = filename.split('-')[2:4]  # Get architecture and platform
        download_url = f"https://github.com/thongtech/go-legacy-win7/releases/download/{tag_name}/{filename}"

        extension = '.'

        for i in ['.zip', '.tar.gz']:
            if filename.endswith(i):
                filename = filename[:-len(i)]
                extension = i
                break

        if ('darwin' in filename) or ('race' in filename) or (extension == '.'):
            continue

        j = filename.split('.')
        platform, arch = j[-1].split('_')
        if platform == 'windows':
            platform = 'win7'
        if arch == 'amd64':
            arch = 'x64'

        files.append({
            "filename": filename + extension,
            "arch": arch,
            "platform": platform,
            "download_url": download_url
        })
    releases.append({
        "version": version,
        "stable": stable,
        "release_url": release_url,
        "files": files
    })

# Generate the JSON structure
json_output = json.dumps(releases, indent=2)

# Print the JSON output
print(json_output)

# Optionally, you can save it to a file
with open("versions-manifest.json", "w") as json_file:
    json_file.write(json_output)

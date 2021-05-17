#!/usr/bin/env bash

# this ensures we have the container image cached locally so docker output doesn't mess up our BOM output
docker run cyclonedx/cyclonedx-cli --version

cp bom-1.3.json boms/bom-1.3.json
docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=json_v1_2 > boms/bom-1.2.json

docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=xml_v1_3 > boms/bom-1.3.xml
docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=xml_v1_2 > boms/bom-1.2.xml
docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=xml_v1_1 > boms/bom-1.1.xml
docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=xml_v1_0 > boms/bom-1.0.xml

docker run --volume "$(pwd)":/files cyclonedx/cyclonedx-cli convert --input-file /files/bom-1.3.json --output-format=spdxtag_v2_2 > boms/bom-2.2.spdx
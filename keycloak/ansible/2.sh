params=$(cat 11.json | jq -r '.groups[].name' | xargs -I {} echo '-d value="{}"' | tr '\n' ' ')
echo $params

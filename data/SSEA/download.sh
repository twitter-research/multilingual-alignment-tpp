# Source: http://ltrc.iiit.ac.in/ner-ssea-08/index.cgi?topic=5

for lang in "hindi" "bengali" "urdu" "telugu" "oriya"; do
    for split in "training" "test"; do
        url="http://ltrc.iiit.ac.in/ner-ssea-08/content/data/${split}-${lang}.zip";
        echo ${url}
        wget ${url}
    done;
done;

# Special processing for telugu dataset
wget http://ltrc.iiit.ac.in/ner-ssea-08/content/data/training-telugu-wx.zip
ls *.zip | xargs -I {} unzip {}
mv training-telugu-wx training-telugu

python process_file.py

for lang in "hindi" "bengali" "urdu" "telugu" "oriya"; do
    cat ./training-${lang}/*.conll > "./training-data-${lang}.conll"
done

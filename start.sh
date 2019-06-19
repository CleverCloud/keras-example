#!/usr/bin/env bash

# Somshubra Majumdar git source
git clone https://github.com/titu1994/Neural-Style-Transfer.git

# Get data source. Picture to process and styles to copy
python get_bucket_content.py $BUCKET_SOURCE $(pwd)/source_images
python get_bucket_content.py $BUCKET_STYLE $(pwd)/style_images

# format arguments to run Somshubra Majumdar's script
style=""
for filename in $(pwd)/style_images/*.jpg; do
	style+=" $filename"
done

# go inside the Somshubra Majumdar's script
cd Neural-Style-Transfer

mkdir results

# process all pictures one by one
i=0
for filename in $(pwd)/../source_images/*.jpg; do
base_filename=$(basename $filename)
prefix=${base_filename::-4}
mkdir results/$prefix

# Somshubra Majumdar' script
python Network.py $filename  $style results/$prefix/$prefix  --num_iter 30  --content_loss_type 0 --image_size 400 --model "vgg16" --rescale_image "yes"
i=$(($i + 1))
done

# tar and send results
tar -zcvf results.tar.gz results
mv results.tar.gz ../
cd ../
python send_to_bucket.py $BUCKET_RESULT results.tar.gz

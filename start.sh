#!/usr/bin/env bash

git clone https://github.com/titu1994/Neural-Style-Transfer.git

python get_bucket_content.py $BUCKET_SOURCE $(pwd)/source_images

python get_bucket_content.py $BUCKET_STYLE $(pwd)/style_images

style=""
for file in $(pwd)/sytle_images/*.jpg; do
tmp="$style $file"
style=$tmp
done

cd Neural-Style-Transfer


mkdir results

i=0
for filename in $(pwd)/../source_images/*.jpg; do
base_filename=$(basename $filename)
prefix=${base_filename::-4}
mkdir results/$prefix
python Network.py $filename  $style results/$prefix/$prefix  --content_weight 5 --style_weight 1.0 1.0 --num_iter 20 --model "vgg16" --content_loss_type 0
i=$(($i + 1))
done


tar -zcvf results.tar.gz results

mv results ../

cd ../

python send_to_bucket.py $BUCKET_RESULT results.tar.gz

#!/usr/bin/env bash

git clone https://github.com/titu1994/Neural-Style-Transfer.git

python get_bucket_content.py $BUCKET_SOURCE $(pwd)/source_images

python get_bucket_content.py $BUCKET_STYLE $(pwd)/style_images

cd Neural-Style-Transfer

while [ true ] ; do
sleep 10
done


mkdir results

for file in $(pwd)/../sytle_images/*.jpg
do
    style=${style:+style }$file
done

i=0
for filename in in $(pwd)/../source_images/*.jpg; do
prefix=$(basename $filename)
python network.py $filename  $style results/result_$i/$prefix  --content_weight 5 --style_weight 1.0 1.0 --num_iter 20 --model "vgg16" --content_loss_type 0
i=$(($i + 1))
done

tar -zcvf results.tar.gz results

mv results ../

cd ../

python send_to_bucket.py $BUCKET_RESULT results.tar.gz

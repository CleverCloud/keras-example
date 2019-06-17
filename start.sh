#!/usr/bin/env bash

while [ true ] ; do
echo "toto"
sleep 10
done

git clone https://github.com/titu1994/Neural-Style-Transfer.git

python get_bucket_content.py $BUCKET_SOURCE $(pwd)/source_images

python get_bucket_content.py $BUCKET_STYLE $(pwd)/style_images

style=""
for filename in $(pwd)/style_images/*.jpg; do
	style+=" $filename"
done

cd Neural-Style-Transfer


mkdir results

i=0
for filename in $(pwd)/../source_images/*.jpg; do
base_filename=$(basename $filename)
prefix=${base_filename::-4}
mkdir results/$prefix
python Network.py $filename  $style results/$prefix/$prefix  --num_iter 30  --content_loss_type 0 --image_size 800 --model "vgg16" --rescale_image
i=$(($i + 1))
done


tar -zcvf results.tar.gz results

mv results.tar.gz ../

cd ../

python send_to_bucket.py $BUCKET_RESULT results.tar.gz

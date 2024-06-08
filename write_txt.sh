# 设定根目录，此处假设脚本位于父文件夹的上一级，你可以根据需要修改此路径
DIR="./lrs2_preprocessed/s1o"

# 设定起始和结束的文件夹序号
START=2698
END=3034

# 输出文件的路径
OUTPUT_FILE="./Wav2Lip_master/filelists/val.txt"

# 清空之前的输出文件内容（如果你不希望清空，而是追加，可以修改这一行）
> "$OUTPUT_FILE"

# 用于存储所有文件路径的数组
declare -a file_paths

# 遍历指定序号范围的文件夹
for (( i=$START; i<=$END; i++ )); do
  # 格式化文件夹序号为5位数字
  FOLDER=$(printf "%05d" $i)
  echo "$FOLDER" >> "$OUTPUT_FILE"

  # 检查文件夹是否存在
#   if [[ -d "$DIR/$FOLDER" ]]; then
#     # 列出所有.jpg文件，并添加到数组
#     for img in "$DIR/$FOLDER"/*.jpg; do
#       if [[ -f "$img" ]]; then
#         # 将相对路径和文件名添加到数组
#         file_paths+=("$FOLDER/$(basename $img)")
#       fi
#     done
#     # 对数组中的文件路径进行排序
#     IFS=$'\n' sorted_paths=($(sort -t '/' -k 2,2n -k 1,1n <<< "${file_paths[*]}"))
#     unset IFS
#     for path in "${sorted_paths[@]}"; do
#       echo "$path" >> "$OUTPUT_FILE"
#     done
#   fi
#   file_paths=()
done


echo "写入完成，输出文件为 $OUTPUT_FILE"
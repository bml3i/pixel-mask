import os
import logging
import ConfigParser
import letterpool

# Setup logging module
logging.basicConfig(filename='log/pixel-mask.log', format='%(levelname)s: %(message)s', level=logging.DEBUG)

# Load configurations
config = ConfigParser.SafeConfigParser()
config.read('pixel-mask.conf')

inputHomePath = config.get('Configuration', 'inputHomePath')
outputHomePath = config.get('Configuration', 'outputHomePath')
inputImageBase64FileName = config.get('Configuration', 'inputImageBase64FileName')
inputPixelWordsFileName = config.get('Configuration', 'inputPixelWordsFileName')
outputFileName = config.get('Configuration', 'outputFileName')

# If inputHomePath and outputHomePath are not configured well
if not os.path.exists(inputHomePath) or (inputHomePath[-1] != os.sep):
  inputHomePath = os.getcwd() + os.sep + "input" + os.sep
if not os.path.exists(outputHomePath) or (outputHomePath[-1] != os.sep):
  outputHomePath = os.getcwd() + os.sep + "output" + os.sep

# read input image base64 string
image_src_base64 = ""
file_input_image_base64 = open(inputHomePath + inputImageBase64FileName, 'r')
for line in file_input_image_base64.readlines():  
  image_src_base64 = line.strip('\n')

image_src_base64_list = list(image_src_base64)
image_src_base64_cursor_idx = 0
image_target_base64_list = []

# read input pixel words
all_pixel_words_list = []
file_input_pixel_words = open(inputHomePath + inputPixelWordsFileName, 'r')
for line in file_input_pixel_words.readlines():  
  all_pixel_words_list.append(line.strip('\n'))

max_pixel_words_length = len(max(all_pixel_words_list, key=len))

for pixel_words_item in all_pixel_words_list:
  curr_pixel_words_item_length = len(pixel_words_item)
  pixel_words_list = list(pixel_words_item)

  for axis_y_idx in range(letterpool.AXIS_Y_RANGE):
    tmp_target_line_str = ""
    for word_idx in range(max_pixel_words_length):
      if word_idx >= curr_pixel_words_item_length: 
        curr_char = " "
      else:
        curr_char = pixel_words_list[word_idx]
      char_line_binary_value = letterpool.LETTER_POOL.get(curr_char)[axis_y_idx]
      for axis_x_idx in range(letterpool.AXIS_X_RANGE):
        cell_binary_value = pow(2, letterpool.AXIS_X_RANGE - 1 - axis_x_idx)
        if char_line_binary_value & cell_binary_value > 0:
          tmp_target_line_str += " "
        else:
          tmp_target_line_str += image_src_base64_list[image_src_base64_cursor_idx]
          image_src_base64_cursor_idx = image_src_base64_cursor_idx + 1
    image_target_base64_list.append(tmp_target_line_str)


# write outputs to file
file_output = open(outputHomePath + outputFileName, 'w')
for line in image_target_base64_list:
  file_output.write("%s\n" % line)

file_output.write("%s\n" % image_src_base64[image_src_base64_cursor_idx:])
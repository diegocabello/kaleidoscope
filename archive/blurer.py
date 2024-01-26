import ffmpeg

input_file = 'forgetmenots.png'
output_file = 'output2.mp4'
duration = 10

# Create the FFmpeg command using ffmpeg-python
(
    ffmpeg
    .input(input_file)
    .filter('scale', 'iw*1.34', 'ih*1.34')
    #.filter_('boxblur', 10)
    .output('temp.mp4', aspect='4:3', t=5)  # Temporary output for blurred background
    .run(overwrite_output=True)
)

(
    ffmpeg
    .input(input_file)
    .output('temp2.mp4', vframes=1)  # Temporary output for foreground
    .run(overwrite_output=True)
)

(
    ffmpeg
    .input('temp.mp4')
    .overlay(ffmpeg.input('temp2.mp4'), x='(main_w-overlay_w)/2', y='(main_h-overlay_h)/2')
    .output(output_file, aspect='4:3', t=duration)
    .run(overwrite_output=True)
)

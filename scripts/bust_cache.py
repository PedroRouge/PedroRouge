import os
import shutil

# Make copies of the newly generated SVGs with clean new filenames to completely bypass GitHub Camo cache
if os.path.exists('contrib-heatmap.svg'):
    shutil.copyfile('contrib-heatmap.svg', 'contrib-heatmap-live.svg')
    print('Created contrib-heatmap-live.svg')

if os.path.exists('whoami.svg'):
    shutil.copyfile('whoami.svg', 'whoami-card.svg')
    print('Created whoami-card.svg')

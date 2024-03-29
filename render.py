import time
import PySide6.QtWidgets
from ovito.io import import_file
from ovito.vis import Viewport, TachyonRenderer, OpenGLRenderer, AnariRenderer
from ovito.modifiers import CommonNeighborAnalysisModifier, SliceModifier


app = PySide6.QtWidgets.QApplication()
PATH = 'D:/Atomsk/Model/合金拉伸/CoNiCr/拉伸/Outputs/30_60_240/CoCrNiTension.xyz'
pipeline = import_file(PATH)  # 轨迹文件
# D:/Atomsk/Model/合金拉伸/CoNiCr/Outputs/75_150_600/CoCrNiTension.xyz

pipeline.add_to_scene()
slice = SliceModifier(enabled=True, distance=120.0, normal=(0, 0, 1), )
pipeline.modifiers.append(slice)
# 先切割，再分析
common = CommonNeighborAnalysisModifier()
pipeline.modifiers.append(common)

vp = Viewport(type=Viewport.Type.Ortho, camera_dir=(1, 0, 0), )  # camera_dir = (0, 0, 1)表示从Z轴方向看去
vp.zoom_all()
start_time = time.time()
vp.render_anim('video_test.mp4', (800, 1200), 60, (1, 1, 1),
               every_nth=2, range=(0, 60), renderer=OpenGLRenderer(antialiasing_level=1))
# OpenGLRenderer(antialiasing_level=1) 抗锯齿级别：1没有，n为n倍超采样
# size决定清晰度，size越大，清晰度越高，如果renderer=TachyonRenderer()表示用cpu渲染，会慢很多，但好像更精致
end_time = time.time()
print(f"Cost time: {end_time - start_time}")

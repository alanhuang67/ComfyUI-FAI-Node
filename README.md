# ComfyUI-FAI-Node

ComfyUI custom node development beginner, focusing on video generation tools. Aim to simplify and optimize the process, enabling easier creation of high-quality video content.

ComfyUI的自定义节点开发新手，主要开发方向是视频生成辅助工具。通过这些节点，希望简化和优化视频生成的流程，让更多人能够轻松地创建高质量的视频内容。


## FAI Dynamic Mask
![image](https://github.com/alanhuang67/ComfyUI-FAI-Node/blob/main/assets/Node_Dynamic_Mask.png).
Easy Mask Generation node


## FAI_Voronoi_Generator
![image](https://github.com/alanhuang67/ComfyUI-FAI-Node/blob/main/assets/Node.png?raw=true)

This is not an entirely new node, but I have revised its function based on my needs, resulting in some very interesting effects.

这并不是一个全新的节点，但我根据自己的需求修改了其功能，产生了一些非常有趣的效果。


### FAI_Voronoi_Generator:

I created 6 new graphic types to generate more effects.

我创建了6种新的图形类型，以产生更多效果。


### FAI_Scale_Scheduler: 

I added 17 formulas for different transitions and turned them into a drop-down menu. This was because I couldn't understand the original formula "0:((15 * cos((a / 60 * 3.141 * (t + 0) / b))**70 + 0.009))", so I created a series of formulas to make things easier.

我添加了17个用于不同过渡效果的公式，并将它们做成了一个下拉菜单。这是因为我不理解原来的公式 "0:((15 * cos((a / 60 * 3.141 * (t + 0) / b))**70 + 0.009))" 。因此，我创建了一系列公式以简化操作。

  
With these two nodes, you can create more intriguing Voronoi effects. Additionally, I have simplified the color mask generation workflow and introduced two-color masks to save VRAM resources and accommodate situations where complex masks aren't needed.

通过这两个节点，你可以创建更有趣的Voronoi效果。此外，我简化了颜色掩码生成流程，并引入了两种颜色掩码，以节省VRAM资源并满足不需要复杂掩码的情况。


**Example workflow**

[Setp1. Example workflow for mask generation](https://github.com/alanhuang67/ComfyUI-FAI-Node/blob/main/example/Step1_Mask_Generation.json)


[Step2. Example workflow for Video generation](https://github.com/alanhuang67/ComfyUI-FAI-Node/blob/main/example/Step2_Video_Generation.json)

Video generation with a two-color mask. Feel free to add more color masks for IPA, and you will need to refine and adjust ControlNet based on your needs.

使用两色掩码进行视频生成。可以根据需要为IPA添加更多颜色遮罩，并根据需要调整和优化ControlNet。


Credit to https://github.com/get-salt-AI/SaltAI_AudioViz and https://discord.com/channels/1076117621407223829/1248723355914473525

(Please let me know if there is anyone I didn't give the credit~)

## INSTALLATION

Git Clone this repo into custom_nodes folder.

Install dependencies: pip install -r requirements.txt (you don't need this if you already install SaltAI_AudioViz node.)



# 使用指南
## ECI部分
 - cid提供的ECI调用接口 https://github.com/cid-harvard/py-ecomplexity
 - 矩阵法计算ECI
 ECI.py
 在小双的数据集上，构建矩阵的时间为1.314秒，计算时间为0.16s
 根据次大特征根的结果
 ![](matrix_2nd_eig_pci.png)
  根据第三大特征根的结果
 ![](matrix_3rd_eig_pci.png)
 
 - 迭代法计算ECI by Yanbo Zhang
 ECIPCI.py
 总时间大概为10s
 ![](iter.png)
 
 ## Trueskill部分
 
 - trueskill.py
 使用实例在true_skill_toy_model.ipynb上面，需要在输入的时候把问题加上标签Q,例如'Q1'
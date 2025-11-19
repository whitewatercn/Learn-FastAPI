"""
本教程学习装饰器decorator的使用
decorator是python的一个重要特性，可以在函数调用前后添加额外的功能，可以用于日志记录、权限验证、性能测试等场景
本质上就是个函数，接收一个函数作为参数，返回一个新的函数
详见 https://forum.beginner.center/t/topic/2396


另外学习annotated type的使用
annotated type是python3.5开始支持的类型注解，可以在类型注解中添加额外的信息，比如范围、正则表达式等，可以用于数据验证、API
需要注意的是，annotated type只是一个类型注解，并不会自动处理数据验证等逻辑，需要配合装饰器或其他方式来实现（比如fastapi的Query、Path等）
"""

from typing import Annotated, get_type_hints,get_origin,get_args
from functools import wraps

# # step1只是有了标注，但是没有任何处理
# def double(x:Annotated[int,(0,100)]) -> int:
# 	return x*2



# # step2有了标注，并且处理成如果不在这个范围，就不执行这个操作
# def double(x:Annotated[int,(0,100)]) -> int:
# 	type_hints = get_type_hints(double,include_extras=True)
# 	hint = type_hints['x']
# 	if get_origin(hint) is Annotated:
# 		hint_type, *hint_args = get_args(hint)
# 		low,high=hint_args[0]
# 		print(hint_type)
# 		print(hint_args)
# 		if not (low <= x <= high):
# 			raise ValueError(f'Value {x} not in range ({low},{high})')
# 	return x*2


# step3 通过装饰器decorator实现step2里的功能
def check_value_range(func):
	@wraps(func)
	def wrapped(x):
		type_hints = get_type_hints(double,include_extras=True)
		hint = type_hints['x']
		if get_origin(hint) is Annotated:
			hint_type, *hint_args = get_args(hint)
			low,high=hint_args[0]
			print(hint_type)
			print(hint_args)
			if not (low <= x <= high):
				raise ValueError(f'Value {x} not in range ({low},{high})')
		return func(x)
	return wrapped

@check_value_range
def double(x:Annotated[int,(0,100)]) -> int:
	return x*2

print(double(150))
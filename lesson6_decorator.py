from typing import Annotated, get_type_hints,get_origin,get_args
from functools import wraps

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


# # step1只是有了标注，但是没有任何处理
# def double(x:Annotated[int,(0,100)]) -> int:
# 	return x*2

print(double(150))
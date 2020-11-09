'''
The main Entry-point of my programs
'''
from app import RouteGenerator

def main():
    route = RouteGenerator()
    route.generate()
    # print(route.__repr__())

if __name__ == '__main__':
    main()
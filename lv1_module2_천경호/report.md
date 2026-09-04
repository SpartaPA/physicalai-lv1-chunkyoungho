# 1. C++ 빌드체계 세우기
## 1. 수동 2단계 빌드 명령
```bash
physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics on  모듈2-시작 [!?] via △ v3.22.1 
➜ g++ -Wall -std=c++17 stop_distance.cpp               

physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics on  모듈2-시작 [!?] via △ v3.22.1 
➜ ls -al
합계 68
drwxrwxr-x 4 pa28 pa28  4096  9월  4 14:41 .
drwxrwxr-x 6 pa28 pa28  4096  9월  4 09:07 ..
-rw-rw-r-- 1 pa28 pa28   446  9월  4 14:23 CMakeLists.txt
-rwxrwxr-x 1 pa28 pa28 29496  9월  4 14:41 a.out
drwxrwxr-x 3 pa28 pa28  4096  9월  4 14:38 build
-rw-rw-r-- 1 pa28 pa28   101  9월  4 13:58 main.cpp
-rw-rw-r-- 1 pa28 pa28   106  9월  4 14:28 motor.cpp
-rw-rw-r-- 1 pa28 pa28   150  9월  4 13:52 motor.hpp
drwxrwxr-x 2 pa28 pa28  4096  8월 25 14:10 sensors
-rw-rw-r-- 1 pa28 pa28  1536  9월  4 13:46 stop_distance.cpp

physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics on  모듈2-시작 [!?] via △ v3.22.1 
➜ ./a.out 10.2 1.1
velocity: 10.2 m/s   decle: 1.1 m/s^2     stop distance: 47.2909 m
```

## 2. 링크에러
```bash
physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics on  모듈2-시작 [!?] via △ v3.22.1 
➜ g++ -c main.cpp motor.cpp

physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics on  모듈2-시작 [!?] via △ v3.22.1 
➜ g++ robot -o main.o
/usr/bin/ld: cannot find robot: 그런 파일이나 디렉터리가 없습니다
collect2: error: ld returned 1 exit status
```

## 3. CMake 빌드 출력
```bash
lv1_module2_천경호/cpp_basics/build on  모듈2-시작 [!?] 
➜ cmake ..
-- The CXX compiler identification is GNU 11.4.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/pa28/kant_gits/physicalai-lv1-chunkyoungho/lv1_module2_천경호/cpp_basics/build
```

## 4. 증분빌드
``` bash
➜ ls -al ./CMakeFiles/robot.dir 
합계 68
drwxrwxr-x 2 pa28 pa28 4096  9월  4 14:28 .
drwxrwxr-x 5 pa28 pa28 4096  9월  4 14:28 ..
-rw-rw-r-- 1 pa28 pa28  768  9월  4 14:23 DependInfo.cmake
-rw-rw-r-- 1 pa28 pa28 6438  9월  4 14:23 build.make
-rw-rw-r-- 1 pa28 pa28  348  9월  4 14:23 cmake_clean.cmake
-rw-rw-r-- 1 pa28 pa28  594  9월  4 14:28 compiler_depend.internal
-rw-rw-r-- 1 pa28 pa28  363  9월  4 14:28 compiler_depend.make
-rw-rw-r-- 1 pa28 pa28  112  9월  4 14:23 compiler_depend.ts
-rw-rw-r-- 1 pa28 pa28   89  9월  4 14:23 depend.make
-rw-rw-r-- 1 pa28 pa28  270  9월  4 14:23 flags.make
-rw-rw-r-- 1 pa28 pa28   88  9월  4 14:23 link.txt
-rw-rw-r-- 1 pa28 pa28 1640  9월  4 14:23 main.cpp.o
-rw-rw-r-- 1 pa28 pa28  252  9월  4 14:23 main.cpp.o.d
-rw-rw-r-- 1 pa28 pa28 1488  9월  4 14:28 motor.cpp.o
-rw-rw-r-- 1 pa28 pa28  254  9월  4 14:28 motor.cpp.o.d
-rw-rw-r-- 1 pa28 pa28   64  9월  4 14:23 progress.make

lv1_module2_천경호/cpp_basics/build on  모듈2-시작 [!?] via △ v3.22.1 
➜ ls -al                       
합계 56
drwxrwxr-x 3 pa28 pa28  4096  9월  4 14:28 .
drwxrwxr-x 4 pa28 pa28  4096  9월  4 14:22 ..
-rw-rw-r-- 1 pa28 pa28 12491  9월  4 14:22 CMakeCache.txt
drwxrwxr-x 5 pa28 pa28  4096  9월  4 14:28 CMakeFiles
-rw-rw-r-- 1 pa28 pa28  6042  9월  4 14:23 Makefile
-rw-rw-r-- 1 pa28 pa28  1738  9월  4 14:23 cmake_install.cmake
-rwxrwxr-x 1 pa28 pa28 16048  9월  4 14:28 robot
```

>.build/CMakeFiles/robot.dir 의 motor.cpp.o와 motor.cpp.o.d, .build/robot 세 파일만 14:28분에 변경된 것을 알 수 있다.
>-> 수정된 파일만 재컴파일이 되며, 증분빌드는 마지막 빌드에서 새롭게 수정된 파일만 컴파일하여 빌드한다는 것을 알 수 있다.

# 2. 현대 C++로 센서 계층 구현
## 1. 다형성 루프 출력

## 2. 스택 객체와 힙 객체의 소멸 시점

## 3. 가상 소명자를 뺏을 때의 차이

## 4. count_if 결과

## 5. 누수 검출 결과
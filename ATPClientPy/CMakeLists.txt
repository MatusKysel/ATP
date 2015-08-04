cmake_minimum_required(VERSION 2.8)

project(ArnoldClient)

option(ONLY_DOC "If set ON, doesn't run CMake for src directory" OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)



############## Platform specific libraries ########

if(ADD_CMAKE_MODULE_PATH)
  set(CMAKE_MODULE_PATH ${ADD_CMAKE_MODULE_PATH})
endif()


################ BOOST ##################
set(Boost_USE_MULTITHREADED TRUE)

set(REQUIRED_BOOST_LIBRARIES
  thread
  system
  filesystem
  program_options
  regex)

if(MSVC)
  list(APPEND REQUIRED_BOOST_LIBRARIES chrono date_time)
  set(Boost_USE_STATIC_LIBS ON)
  add_definitions(-DBOOST_ALL_NO_LIB)
endif(MSVC)


if(BUILD_DIR AND NOT BOOST_ROOT)
  set(BOOST_ROOT ${BUILD_DIR})
endif()
find_package(Boost COMPONENTS ${REQUIRED_BOOST_LIBRARIES} REQUIRED)

include_directories(${Boost_INCLUDE_DIR})

if(${Boost_MINOR_VERSION} VERSION_GREATER 49)
  add_definitions(-DOTS_BOOST_THREAD_EXTENSION)
endif()
################ BOOST ##################

################ OPENSSL ################
#if(NOT NO_OPENSSL)
  if(BUILD_DIR AND NOT OPENSSL_ROOT_DIR)
    set(OPENSSL_ROOT_DIR ${BUILD_DIR})
  endif()

  find_package(OpenSSL)
#  if(OPENSSL_FOUND)
    include_directories(${OPENSSL_INCLUDE_DIR})
#  else()
#    add_definitions(-DOTS_NO_OPENSSL)
#    set(NO_OPENSSL 1)
#    message(WARNING "OpenSSL not found")
#  endif()
#else()
#  add_definitions(-DOTS_NO_OPENSSL)
#  message(STATUS "Skipping OpenSSL")
#endif()
################ OPENSSL ################

################ THREADS ################
find_package(Threads REQUIRED)
################ THREADS ################

include(CheckCXXSourceCompiles)
set(CMAKE_REQUIRED_INCLUDES ${Boost_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_REQUIRED_LIBRARIES ${Boost_LIBRARIES})

set(THIRD_LIBRARIES ${PLATFORM_LIBS} ${Boost_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT} ${OPENSSL_LIBRARIES} ${CMAKE_DL_LIBS})


add_executable(ArnoldClient main.cc client.cc client.h)
target_link_libraries(ArnoldClient ${THIRD_LIBRARIES})





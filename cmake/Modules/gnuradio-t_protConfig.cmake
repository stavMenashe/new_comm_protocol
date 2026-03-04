find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_T_PROT gnuradio-t_prot)

FIND_PATH(
    GR_T_PROT_INCLUDE_DIRS
    NAMES gnuradio/t_prot/api.h
    HINTS $ENV{T_PROT_DIR}/include
        ${PC_T_PROT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_T_PROT_LIBRARIES
    NAMES gnuradio-t_prot
    HINTS $ENV{T_PROT_DIR}/lib
        ${PC_T_PROT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-t_protTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_T_PROT DEFAULT_MSG GR_T_PROT_LIBRARIES GR_T_PROT_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_T_PROT_LIBRARIES GR_T_PROT_INCLUDE_DIRS)

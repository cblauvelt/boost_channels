from conans import ConanFile, CMake, tools


class BoostChannelsConan(ConanFile):
    name = "boost_channels"
    version = "master"
    license = "Boost Software License"
    author = "Richard Hodges (hodges.r@gmail.com)"
    url = "https://github.com/madmongo1/boost_channels"
    description = "Experimental library to test feasabiltity of go-like channels built on Asio"
    topics = ("boost", "asio", "async", "channel")
    exports_sources = ["CMakeLists.txt", "conanfile.py", "include/*", "examples/*", "test/*"]
    settings = "os", "compiler", "build_type", "arch"
    requires = "boost/1.77.0"
    build_requies = "doctest/2.4.6"
    options = {"cxx_standard": [20], "build_testing": [True, False], "build_examples": [True, False]}
    default_options = {"cxx_standard": 20, "build_testing": True, "build_examples": True}
    generators = "cmake", "cmake_paths", "cmake_find_package"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def sanitize_version(self, version):
        return re.sub(r'^v', '', version)


    def set_version(self):
        git = tools.Git(folder=self.recipe_folder)
        self.version = self.sanitize_version(git.get_tag()) if git.get_tag() else "%s_%s" % (git.get_branch(), git.get_revision())

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = self.options.build_testing
        cmake.definitions["BOOST_CHANNELS_BUILD_TESTS"] = self.options.build_examples
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = "conan_paths.cmake"
        cmake.configure()
        cmake.build()
        cmake.test()

    def package(self):
        self.copy("LICENSE", dst="licenses")
        self.copy("*.hpp", dst="include", src="include")
        # self.copy("*.hpp", dst="include", src="include/boost")
        # self.copy("*.hpp", dst="include", src="include/boost/channels")
        # self.copy("*.hpp", dst="include", src="include/boost/channels/concepts")
        # self.copy("*.hpp", dst="include", src="include/boost/channels/detail")
        # self.copy("*.hpp", dst="include", src="include/boost/channels/impl")

    def package_info(self):
        self.info.header_only()

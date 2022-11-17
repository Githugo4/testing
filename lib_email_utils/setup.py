import setuptools


# from pip.req import parse_requirements
# pip install pipreqs

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [str(line) for line in lineiter if line and not line.startswith("#")]


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

setuptools.setup(
    name='Email_SMTP_UTIL',
    packages=['emaillib'],
    data_files=[(".", ["requirements.txt"])],
    description='Homefats Libraries',
    version='0.1',
    author='Homefacts',
    include_package_data=True,
    author_email='homefactsinfra@gmail.com',
    keywords=['pip', 'homefacts'],
    install_requires=install_reqs,
    long_description="test",
    long_description_content_type="text/markdown",
)

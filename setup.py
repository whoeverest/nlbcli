import setuptools

setuptools.setup(
    name="nlbcli", # Replace with your own username
    version="0.0.1",
    author="Andrej Trajchevski",
    author_email="andrejtrajchevski@gmail.com",
    description="A CLI for nlbklik.com.mk -- check your balance, list transactions and such.",
    url="https://github.com/whoeverest/nlbcli/",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    entry_points = {
        'console_scripts': ['nlbcli=nlbcli.__main__:main']
    },
    install_requires=[
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.3'
    ],
    package_data={
        "nlbcli": ["*.pem"]
    }
)

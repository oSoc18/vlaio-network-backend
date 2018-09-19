import os.path

print(
    os.path.abspath(
        os.path.join(
            os.path.join(
                os.path.join(
                    __file__,
                    os.path.pardir
                ),
                os.path.pardir
            ),
            'sql_scripts'
        )
    )
)

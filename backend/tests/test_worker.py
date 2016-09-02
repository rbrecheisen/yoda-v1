from service.compute.worker import run_pipeline


def run():
    result = run_pipeline.apply_async((1, {
        'file_id': 1,
    }))
    print(result)


if __name__ == '__main__':
    run()

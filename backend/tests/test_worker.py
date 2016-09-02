from service.compute.worker import run_pipeline


def run():
    run_pipeline.apply_async((1, {
        'file_id': 1,
    }))


if __name__ == '__main__':
    run()

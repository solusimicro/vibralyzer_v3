from diagnostic_l2.diagnostic_engine import run_diagnostic


def l2_worker(job: dict):
    """
    job = {
        asset,
        point,
        window,
        publisher
    }
    """
    asset = job["asset"]
    point = job["point"]
    window = job["window"]
    publisher = job["publisher"]

    result = run_diagnostic(window)

    publisher.publish_l2_result(
        asset,
        point,
        result,
    )

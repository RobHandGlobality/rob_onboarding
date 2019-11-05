from microcosm.loaders import (
    load_each,
    load_from_dict,
    load_from_environ,
    load_from_json_file,
)
from microcosm_pubsub.daemon import ConsumerDaemon

import rob_onboarding.daemon.handlers  # noqa: F401


class RobOnboardingOrdersDaemon(ConsumerDaemon):
    @property
    def name(self):
        return "rob_onboarding"

    @property
    def loader(self):
        return load_each(
            load_from_dict(self.defaults), load_from_environ, load_from_json_file,
        )

    @property
    def components(self):
        return super().components + [
            # handlers
            "order_fulfilled_handler",
        ]


def main():
    daemon = RobOnboardingOrdersDaemon()
    daemon.run()


if __name__ == "__main__":
    main()

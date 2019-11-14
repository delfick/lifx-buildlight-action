LIFX Github Action buildight
============================

This is a github action you can use to make your lights respond to github events.

To use, put a file in .github/workflows in your repository that looks
something like:

.. code-block:: yml

    ---

    name: Blink light
    on: [push]
    jobs:
    blink:
      name: Blink
      runs-on: ubuntu-latest
      steps:
        - name: lifx-buildlight
          uses: delfick/lifx-buildlight-action@v1
          env:
            LIFX_TOKEN: "${{ secrets.LIFX_TOKEN }}"
            SELECTOR: label:strip
            BODY: '{"power": "on", "color": "green"}'

For this to work, you must go to https://cloud.lifx.com/settings and create an
api token. Then add to your repository a secret called ``LIFX_TOKEN`` with
the token you have created.

Options
-------

There are a few options available to you that you can set as environment variables.

SELECTOR
    This is the light(s) that you want to change when the action happens.

    It defaults to ``all``

    More information can be found at https://api.developer.lifx.com/docs/selectors

ACTION_TYPE
    This defaults to ``state`` and can be one of the following options based on
    which endpoint to use: https://api.developer.lifx.com/docs/introduction

    state
        https://api.developer.lifx.com/docs/set-state

    states
        https://api.developer.lifx.com/docs/set-states

    effect
        One of the effect endpoints, where the endpoint to use is determined
        by the ``effect`` option in ``BODY``

        https://api.developer.lifx.com/docs/breathe-effect

        https://api.developer.lifx.com/docs/move-effect

        https://api.developer.lifx.com/docs/morph-effect

        https://api.developer.lifx.com/docs/flame-effect

        https://api.developer.lifx.com/docs/pulse-effect

        https://api.developer.lifx.com/docs/effects-off

    cycle
        https://api.developer.lifx.com/docs/cycle

    toggle
        https://api.developer.lifx.com/docs/toggle-power

    scene
        https://api.developer.lifx.com/docs/activate-scene

BODY
    A json string representing the  body of the request.

    It defaults to ``{}``.

    Note that if ``ACTION_TYPE`` is ``effect``, then you must specify
    ``effect`` in the body.

    For example:

    .. code-block:: yml

        BODY: '{"effect": "morph"}'

Examples
--------

You could activate a scene with something like:

.. code-block:: yml

    env:
      SELECTOR: scene_id:4a2d36ac-90af-4a4a-83e0-a25e0d76b2e1
      ACTION_TYPE: scene

You could make your light blink a few times with something like:

.. code-block:: yml

    env:
      SELECTOR: label:my_amazing_light
      ACTION_TYPE: effect
      BODY: '{"effect": "pulse", "color": "red", "from_color": "blue", "cycles": 3}'

Or you could make your light turn green with something like:

.. code-block:: yml

    env:
      SELECTOR: group:desk
      BODY: '{"power": "on", "color": "green"}'

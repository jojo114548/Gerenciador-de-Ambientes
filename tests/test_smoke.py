def test_pytest_funciona():
    assert True


def test_import_controllers():
    import controller.ambiente_controller
    import controller.evento_controller
    import controller.equipamento_controller
    import controller.usuario_controller

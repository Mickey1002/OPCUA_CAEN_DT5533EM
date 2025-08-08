def initialize_register_variables(set_vars):
    for ch, ch_vars in set_vars.items():
        ch_vars['VSET'].set_value(0.0)
        ch_vars['ISET'].set_value(3000.0)
        ch_vars['IMRANGE'].set_value("HIGH")
        ch_vars['RUP'].set_value(100)
        ch_vars['RDW'].set_value(100)
        ch_vars['PDWN'].set_value("RAMP")
        ch_vars['ON'].set_value(False)
        ch_vars['OFF'].set_value(True)
        ch_vars['MAXV'].set_value(2000.0)
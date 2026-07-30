from first_run import first_run_check, pandas_companies, ports


def seperation():
    driver1, driver2, driver3, driver4, company1, company2, company3, company4 = first_run_check()
    df1, df2, df3, df4 = pandas_companies(company1, company2, company3, company4)
    port1, port2, port3, port4, port5, port6, port7, port8 = ports()
    return df1, df2, df3, df4, port1, port2, port3, port4, port5, port6, port7, port8, driver1, driver2, driver3,\
        driver4

import datetime
from unittest import TestCase
from lexnlp.extract.en.dates import get_raw_date_list, get_dates_list


class TestDatesPlain(TestCase):

    def test_dates(self):
        text = """
        2. Amendment to Interest Rate. Beginning on February 1, 1998, and
                continuing until July 18, 2002, which is the fifth anniversary of the Loan
                conversion date, interest shall be fixed at an annual rate of 7.38%, which rate
                is equal to 200 basis points above the Bank's five-year ""Treasury Constant
                Rate"" in effect on January 23, 1998. In accordance with the Agreement, the
                interest rate shall be adjusted again on July 18, 2002.
        """
        dates = get_raw_date_list(text)
        self.assertEqual(4, len(dates))
        self.assertEqual(datetime.date(1998, 2, 1), dates[0])
        self.assertEqual(datetime.date(2002, 7, 18), dates[1])
        self.assertEqual(datetime.date(1998, 1, 23), dates[2])
        self.assertEqual(datetime.date(2002, 7, 18), dates[3])

    def test_dates_times(self):
        text = "From 12:01 a.m. on March 1, 1999 (the 'Commencement Date') through " +\
               "1l:59 p.m. on November 30, 2002 (the 'Expiration Date')"
        dates = get_raw_date_list(text)

        self.assertEqual(2, len(dates))
        self.assertEqual(datetime.datetime(1999, 3, 1, 0, 1), dates[0])
        self.assertEqual(datetime.date(2002, 11, 30), dates[1])

    def test_moar_dates(self):
        text = """
        2. Amendment to Interest Rate. Beginning on February 1, 1998, and
        continuing until July 18, 2002, which is the fifth anniversary of the Loan
        conversion date, interest shall be fixed at an annual rate of 7.38%, which rate
        is equal to 200 basis points above the Bank's five-year "Treasury Constant
        Rate" in effect on January 23, 1998. In accordance with the Agreement, the
        interest rate shall be adjusted again on July 18, 2002.
        """

        dates = get_dates_list(text)
        self.assertEqual(4, len(dates))

    def no_test_no_dates(self):
        text = """
        18.1 Methods of Application 1-57 18.2 Issue of Certificate of payment 1-57 18.3
                           Corrections to Certificates of Payment 1-58 18.4 Payment 1-58 18.5 Delayed Payment 1-58
                           18.6 Remedies on Failure to Certify or Make Payment 1-58 18.7 Application for Final
                           Certificate of Payment 1-59 18.8 Issue of final Certificate of Payment 1-59 18.9 Final
                           Certificate of Payment conclusive 1-60 18.10 Advance Payment 1-60 18.11 Advance Payment
                           Guarantee 1-60 18.12 Terms of Payment 1-60 18.13 Retention 1-61
        """
        dates = get_raw_date_list(text)
        self.assertEqual(len(dates), 0)

    def test_more_more_dates(self):
        text = """
        In the event the real estate taxes levied or assessed against the land
                       and building of which the premises are a part in future tax years are
                       greater than the real estate taxes for the base tax year, the TENANT,
                       shall pay within thirty (30) days after submission of the bill to TENANT for the increase in
                       real estate taxes, as additional rent a proportionate share of such
                       increases, which proportionate share shall be computed at 22.08% of the
                       increase in taxes, but shall exclude any fine, penalty, or interest
                       charge for late or non-payment of taxes by LANDLORD. The base tax year
                       shall be July 1, 1994 to June 30, 1995.
        """
        dates = get_dates_list(text)
        self.assertEqual(2, len(dates))

    def test_two_ranges(self):
        text = """
        be July 1, 1994 to June 30, 1995 through 10/07/1998
        """
        dates = get_dates_list(text)
        self.assertEqual(len(dates), 3)

    def test_two_dates_strict(self):
        text = """
            This monthly maintenance and support arrangement will have an initial term of six (6)
            months. The arrangement will then automatically renew for an additional twelve (12) months
            at the above rates and conditions unless written notification to US/INTELICOM of Licensee's
            intent to cancel the arrangement is received no later than September 1, 1998. Unless
            Licensee elects to cancel this arrangement at the end of the first six months, the "initial
            term" of the arrangement will be through September 30, 1999.
        """
        dates = get_dates_list(text)
        self.assertEqual(2, len(dates))
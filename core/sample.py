class Sample:
    """
    Хранит шаблон письма для рассылки,
    в который затем подставляются спарсенные
    данные.
    """

    HTML_SAMPLE = {
        'text':
            """\
            <html>
              <body>
                <div style="font-family:tahoma,sans-serif">
                <p>
                  <var>holder</var>
                </p>
                <br>
                <p>
                  Dear Sirs,
                </p>
                <p>
                  Trademark <b><var>trade_mark</var></b>, international
                   registration No. <var>reg_num</var>, has been
                   provisionally refused in Russia.
                </p>
                <p>
                  The deadline to respond to the provisional refusal is <b>six
                   months from the date of the provisional refusal</b>.<br>
                  This term cannot be suspended, extended or further
                   restored. Depending on the basis for a provisional refusal,
                  non-responding can lead to a final refusal.
                </p>
                <p>
                  We will be happy to analyse the issued provisional refusal
                  and offer ways to overcome it. Our recommendations will
                  be prepared on a courtesy basis free of charge.
                </p>
                <p>
                  According to the Russian Civil Code, foreign applicants
                  need to assign a local trademark attorney to communicate
                  with the Russian Patent and Trademark Office (Rospatent).
                </p>
                <p>
                  Versus.legal is an international consulting company, offering
                  legal services in different fields, including intellectual
                  property. We have local branches in Russia, UAE, Hong Kong,
                  and CIS countries.
                </p>
                <p>
                  Our Russian IP branch has a team of certified trademark
                  attorneys, who assist international partners with overcoming
                  provisional refusals and handling other trademark cases.
                </p>
                <p>
                  If you need help with drawing up a strategy to overcome
                  the provisional refusal and respond to it, please
                  feel free to contact us for further details.
                </p>
                <p>Best regards,<br>
                  Versus.legal team
                </div>
                </p>
                <div style="background:white;color:rgb( 26 , 26 , 26 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:14.5pt;margin:0cm 0cm 0.0001pt 0cm;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><br>
                </div>
                <div>--&nbsp;</div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:19.36px;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">
                <img data-cke-saved-src="https://avatars.mds.yandex.net/get-mail-signature/474754/046ee2320acf907274c2755ce77d1331/orig" src="https://avatars.mds.yandex.net/get-mail-signature/474754/046ee2320acf907274c2755ce77d1331/orig" style="height:32px;width:133px">
                </div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:19.36px;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><u><span style="color:black;font-family:'verdana' , sans-serif;font-size:7.5pt">wipo@versus.legal</span></u></div>
                <br>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">CONFIDENTIALITY NOTICE: The contents of this email message </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and any attachments are intended solely for the addressee(s) </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and may contain confidential and/or privileged information </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and may be legally protected from disclosure.</span></font></div>
              </body>
            </html>
            """,
    }

    HTML_SAMPLE_MULT = {
        'text':
            """\
            <html>
              <body>
                <div style="font-family:tahoma,sans-serif">
                <p>
                  <var>holder</var>
                </p>
                <br>
                <p>
                  Dear Sirs,
                </p>
                <p>
                  Trademarks <b><var>trade_mark</var></b>, international
                   registration No. <var>reg_num</var>, have been
                   provisionally refused in Russia.
                </p>
                <p>
                  The deadline to respond to the provisional refusal is <b>six
                   months from the date of the provisional refusal</b>.<br>
                  This term cannot be suspended, extended or further
                   restored. Depending on the basis for a provisional refusal,
                  non-responding can lead to a final refusal.
                </p>
                <p>
                  We will be happy to analyse the issued provisional refusals
                  and offer ways to overcome them. Our recommendations will
                  be prepared on a courtesy basis free of charge.
                </p>
                <p>
                  According to the Russian Civil Code, foreign applicants
                  need to assign a local trademark attorney to communicate
                  with the Russian Patent and Trademark Office (Rospatent).
                </p>
                <p>
                  Versus.legal is an international consulting company, offering
                  legal services in different fields, including intellectual
                  property. We have local branches in Russia, UAE, Hong Kong,
                  and CIS countries.
                </p>
                <p>
                  Our Russian IP branch has a team of certified trademark
                  attorneys, who assist international partners with overcoming
                  provisional refusals and handling other trademark cases.
                </p>
                <p>
                  If you need help with drawing up a strategy to overcome
                  the provisional refusals and respond to them, please
                  feel free to contact us for further details.
                </p>
                <p>Best regards,<br>
                  Versus.legal team
                </div>
                </p>
                <div style="background:white;color:rgb( 26 , 26 , 26 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:14.5pt;margin:0cm 0cm 0.0001pt 0cm;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><br>
                </div>
                <div>--&nbsp;</div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:19.36px;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">
                <img data-cke-saved-src="https://avatars.mds.yandex.net/get-mail-signature/474754/046ee2320acf907274c2755ce77d1331/orig" src="https://avatars.mds.yandex.net/get-mail-signature/474754/046ee2320acf907274c2755ce77d1331/orig" style="height:32px;width:133px">
                </div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-family:'calibri' , sans-serif;font-size:11pt;font-style:normal;font-weight:400;line-height:19.36px;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><u><span style="color:black;font-family:'verdana' , sans-serif;font-size:7.5pt">wipo@versus.legal</span></u></div>
                <br>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">CONFIDENTIALITY NOTICE: The contents of this email message </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and any attachments are intended solely for the addressee(s) </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and may contain confidential and/or privileged information </span></font></div>
                <div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 0 , 0 , 0 );font-style:normal;font-weight:400;margin-bottom:0.0001pt;text-decoration-color:initial;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px"><font face="verdana, sans-serif"><span style="font-size:8px">and may be legally protected from disclosure.</span></font></div>
              </body>
            </html>
            """,
    }

    VARS = ['holder', 'reg_num', 'trade_mark', ]


            21: network.run_ftp_scanning,
            22: network.run_ssh_scanning,
            23: network.run_telnet_scanning,
            25: network.run_smtp_scanning,
            53: network.run_dns_scanning,
            3389: network.run_rdp_scanning
        }.get(port, None)

        if scan_function:
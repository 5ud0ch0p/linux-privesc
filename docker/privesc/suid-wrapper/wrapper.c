int main()
{
	setuid(0);
	setgid(0);
	// python3 required below to work with some Windows Docker hosts
	system("python3 /home/lowpriv/privesc/privescs.py");
	return 0;
}

